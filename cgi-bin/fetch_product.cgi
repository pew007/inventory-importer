#!/usr/bin/perl

use CGI;
use CGI::Carp qw (fatalsToBrowser);
use JSON;
use DBI;

####################################################################
### constants
my $upload_dir = '/home/vagrant/public_html/proj1/_p_images';
my $safe_filename_chars = "a-zA-Z0-9_.-";
####################################################################

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

    my ($status) = @_;

    my $json->{"result"} = $status;
    my $json_text = to_json($json);

    print $cgi->header('application/json');

    print $json_text;
}
