#!/usr/bin/perl

use CGI;
use CGI::Session;
use CGI::Carp qw (fatalsToBrowser);
use Crypt::SaltedHash;
use DBI;
use Session::Token;
use HTML::Template;
use strict;
use warnings;

my $cgi = new CGI;
# my $host = "opatija.sdsu.edu";
# my $username = "jadrn048";
# my $password = "outlet";
my $host = '127.0.0.1';
my $port = "3306";
my $database = "jadrn048";
my $username = 'root';
my $password = "";
my $database_source = "dbi:mysql:$database:$host:$port";

print $cgi->header;

render_main();

sub render_main {
    my $vendors     = get_all('vendor');
    my $categories  = get_all('category');
    my $platforms   = get_all('platform');
    my $products    = get_products();

    # instantiate the template and substitute the values
    my $template = HTML::Template->new(filename => '/vagrant/templates/main.tmpl');
    $template->param(
        VENDORS     => $vendors,
        CATEGORIES  => $categories,
        PLATFORMS   => $platforms,
        PRODUCTS    => $products
    );

    print $template->output;
}

sub get_all {
    my ($table) = @_;

    my $dbh = DBI->connect($database_source, $username, $password) or die 'Cannot connect to db';
    my $sth = $dbh->prepare("SELECT * FROM $table");
    $sth->execute();
    my $results;
    push @{$results}, $_ while $_ = $sth->fetchrow_hashref();

    $sth->finish();
    $dbh->disconnect();

    return $results;
}

sub get_products {
    my $dbh = DBI->connect($database_source, $username, $password) or die 'Cannot connect to db';
    my $statement = "
        SELECT sku, vendorModel, description, features, cost, retail, image, categoryName, vendorName, platformName
        FROM product, category, platform, vendor
        WHERE category.categoryID = product.categoryID
        AND platform.platformID = product.platformID
        AND vendor.vendorID = product.vendorID";

    my $sth = $dbh->prepare($statement);
    $sth->execute();
    my $results;
    push @{$results}, $_ while $_ = $sth->fetchrow_hashref();

    $sth->finish();
    $dbh->disconnect();

    return $results;
}
