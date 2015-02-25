#!/usr/bin/perl

use CGI;
use CGI::Carp qw (fatalsToBrowser);
use JSON;
use DBI;

my $upload_dir = '/home/vagrant/public_html/proj1/_p_images';

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

my $filename = $upload_dir . "/" . lc($sku) . ".jpg";
unlink($filename);

my $dbh = DBI->connect($database_source, $username, $password)
or die 'Cannot connect to db';

my $statement = "DELETE FROM product WHERE sku = '$sku'";
my $rows = $dbh->do($statement);
$dbh->disconnect();

if ($rows > 0) {
    get_json_response('OK');
} else {
    get_json_response('Error');
}

sub get_json_response {

    my ($status) = @_;

    my $json->{"status"} = $status;
    my $json_text = to_json($json);

    print $cgi->header('application/json');

    print $json_text;
}
