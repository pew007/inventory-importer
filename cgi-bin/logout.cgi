#!/usr/bin/perl

use CGI;
use CGI::Session;
use CGI::Carp qw (fatalsToBrowser);

my $cgi = new CGI;
my $cookie_sid = $cgi->cookie("jadrn048SID") || undef;

$session = new CGI::Session(undef, $cookie_sid, {Directory => '/tmp'});
# $session->delete();
$session->clear(['token']);

print $cgi->header(
    '-cookie'        => $cgi->cookie(jadrn048SID => $session->id),
    '-Cache-Control' => 'must-revalidate, max-age=0, no-store, no-cache'
    );


print "session id is " . $session->id . "<br><br>";
print "token in session is " . $session->param('token');
# print <<END

# <html>
# <head>
#     <meta http-equiv="refresh" content="0; url=http://localhost:8081/index.html">
# </head>
# </html>

# END
