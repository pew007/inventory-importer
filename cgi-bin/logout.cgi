#!/usr/bin/perl

use CGI;
use CGI::Session;
use CGI::Carp qw (fatalsToBrowser);

my $cgi = new CGI;
my $cookie_sid = $cgi->cookie("jadrn048SID") || undef;

$session = new CGI::Session(undef, $cookie_sid, {Directory => '/tmp'});
$session->delete();

my $cookie = $cgi->cookie(jadrn048SID => '');
print $cgi->header( -cookie=>$cookie );


# Redirect back to main.cgi and since the cookie doesn't have a valid session id
# authentication will fail thus preventing the user to go back to the previous page
print <<END

<html>
<head>
    <meta http-equiv="refresh" content="0; url=http://jadran.sdsu.edu/cgi-bin/jadrn048/main.cgi">
</head>
</html>

END
