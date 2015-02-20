#!/usr/bin/perl

use CGI;
use CGI::Session;
use CGI::Carp qw (fatalsToBrowser);

my $cgi = new CGI;
my $sid = $cgi->cookie("jadrn048SID") || undef;

$session = new CGI::Session(undef, $sid, {Directory => '/tmp'});
$session->clear(['token']);
# $session->delete();

my $cookie = $cgi->cookie(jadrn048SID => '');

print $cgi->header( -cookie => $cookie );


print "Token is " . $session->param('token') . "<br>";
print <<END

<html>
<head>

</head>
<body>
<h2>You are logged out<h2>
</body>
</html>

END
