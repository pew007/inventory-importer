#!/usr/bin/perl

use CGI;
use CGI::Session;
use CGI::Carp qw (fatalsToBrowser);

my $cgi = new CGI;
my $sid = $cgi->cookie("jadrn048SID") || undef;

$session = new CGI::Session(undef, $sid, {Directory => '/tmp'});
$session->delete();

my $cookie = $cgi->cookie(jadrn048SID => '');

print $cgi->header(
    -cookie => $cookie,
    '-Cache-Control' => 'must-revalidate, max-age=0, no-store, no-cache'
    );


print <<END

<html>
<head>
    <meta http-equiv="refresh" content="0; url=http://localhost:8081/index.html">
</head>
</html>

END
