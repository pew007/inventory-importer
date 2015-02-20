#!/usr/bin/perl

use CGI;
use CGI::Session;
use CGI::Carp qw (fatalsToBrowser);
use Crypt::SaltedHash;

my $q = new CGI;
my $cookie_sid = $q->cookie('jadrn000SID');
my $session = new CGI::Session(undef, $cookie_sid, {Directory=>'/tmp'});
my $sid = $session->id;

if($cookie_sid ne $sid) {
    print <<END;
Content-type:  text/html

<html>
<head>
    <meta http-equiv="refresh" 
        content="0; url=http://jadran.sdsu.edu/~jadrn000/proj1_examples/sessions_cookies/error.html" />
</head><body></body>
</html>

END
return;
}

print <<END;
Content-type: text/html

<html>
<head>
    
</head>
<body>
<h2>This is PAGE #1</h2>
<p>
<ul>
<li><a href="/perl/jadrn000/proj1/sessions_cookies/page1.cgi">First Page</a></li>
<li><a href="/perl/jadrn000/proj1/sessions_cookies/page2.cgi">Second Page</a></li>
<li><a href="/perl/jadrn000/proj1/sessions_cookies/page3.cgi">Third Page</a></li>
<li><a href="/perl/jadrn000/proj1/sessions_cookies/page4.cgi">Fourth Page</a></li>
</ul>
</p>


<table>
    <tr>
        <td>The current session ID is</td>
        <td>$sid</td>
    </tr>
    <tr>
        <td>The cookie session ID is</td>
        <td>$cookie_sid</td>
    </tr>
</table>


<br />
<a href="/perl/jadrn000/proj1/sessions_cookies/logout.cgi">Logout Now</a>
</body>
</html>

END
