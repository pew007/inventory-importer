#!/usr/bin/perl

use CGI;
use CGI::Session;
use CGI::Carp qw (fatalsToBrowser);
use JSON;
use DBI;

my $upload_dir = '/home/jadrn048/public_html/proj1/_p_images';

my $host = "opatija.sdsu.edu";
my $username = "jadrn048";
my $password = "outlet";
my $port = "3306";
my $database = "jadrn048";
my $database_source = "dbi:mysql:$database:$host:$port";

my $cgi = new CGI;
my $sku = $cgi->param('sku');

my $filename = $upload_dir . "/" . lc($sku) . ".jpg";
unlink($filename);

print $cgi->header;

if (validate_session()) {
    my $dbh = DBI->connect($database_source, $username, $password)
    or die 'Cannot connect to db';

    my $statement = "DELETE FROM product WHERE sku = '$sku'";
    my $rows = $dbh->do($statement);
    $dbh->disconnect();

    if ($rows > 0) {
        get_json_response('OK', 'Product removed.');
    } else {
        get_json_response('Error', 'Failed to remove product.');
    }
} else {
    get_json_response('SessionError', 'Invalid session.');
}

sub get_json_response {
    my ($status, $message) = @_;

    my %response_hash = ('status' => $status, 'message' => $message);
    my $json = encode_json \%response_hash;

    print $json;
}

sub validate_session {
    my $cookie_sid = $cgi->cookie('jadrn048SID');
    my $session = new CGI::Session(undef, $cookie_sid, {Directory=>'/tmp'});
    my $sid = $session->id;

    if($cookie_sid ne $sid) {
        return 0;
    } else {return 1;}
}
