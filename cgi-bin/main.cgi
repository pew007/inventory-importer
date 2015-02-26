#!/usr/bin/perl

use CGI;
use CGI::Session;
use CGI::Carp qw (fatalsToBrowser);
use Crypt::SaltedHash;
use DBI;
use HTML::Template;
use strict;
use warnings;

my $host = "opatija.sdsu.edu";
my $username = "jadrn048";
my $password = "outlet";
my $port = "3306";
my $database = "jadrn048";
my $database_source = "dbi:mysql:$database:$host:$port";

my $cgi = new CGI;
print $cgi->header;

if (validate_session()) {
    render_main();
} else {
    send_to_login_error();
}

sub validate_session {
    my $cookie_sid = $cgi->cookie('jadrn048SID');
    my $session = new CGI::Session(undef, $cookie_sid, {Directory=>'/tmp'});
    my $sid = $session->id;

    if($cookie_sid ne $sid) {
        return 0;
    } else {return 1;}
}

sub send_to_login_error {
    print <<END;
Content-type:  text/html

<html>
<head>
    <meta http-equiv="refresh"
        content="0; url=http://jadran.sdsu.edu/~jadrn048/proj1" />
</head><body></body>
</html>

END
}

sub render_main {
    my $vendors     = get_all('vendor');
    my $categories  = get_all('category');
    my $platforms   = get_all('platform');
    my $products    = get_products() || [];

    # instantiate the template and substitute the values
    my $template = HTML::Template->new(filename => '/home/jadrn048/public_html/proj1/templates/main.tmpl');
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
