#!/usr/bin/perl

use CGI;
use CGI::Carp qw (fatalsToBrowser);
use JSON;
use DBI;

# my $host = "opatija.sdsu.edu";
# my $username = "jadrn048";
# my $password = "outlet";
my $host = '127.0.0.1';
my $port = "3306";
my $database = "jadrn048";
my $username = 'root';
my $password = "";
my $database_source = "dbi:mysql:$database:$host:$port";

my $cgi = new CGI;
my $sku = $cgi->param('sku');

my $dbh = DBI->connect($database_source, $username, $password)
or die 'Cannot connect to db';

my $statement = "
        SELECT sku, vendorModel, description, features, cost, retail, image, product.categoryID, categoryName, product.vendorID, vendorName,product.platformID, platformName
        FROM product, category, platform, vendor
        WHERE product.sku = '$sku'
        AND category.categoryID = product.categoryID
        AND platform.platformID = product.platformID
        AND vendor.vendorID = product.vendorID";

my $sth = $dbh->prepare($statement);
$sth->execute();
my $results;
push @{$results}, $_ while $_ = $sth->fetchrow_hashref();

$sth->finish();
$dbh->disconnect();

get_json_response($results);

sub get_json_response {

    my ($result) = @_;

    my $json->{"result"} = $result;
    my $json_text = to_json($json);

    print $cgi->header('application/json');

    print $json_text;
}
