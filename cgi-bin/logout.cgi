#!/usr/bin/perl

use CGI;
use CGI::Session;
use CGI::Carp qw (fatalsToBrowser);

my $q = new CGI;
my $sid = $q->cookie("jadrn000SID") || undef;

$session = new CGI::Session(undef, $sid, {Directory => '/tmp'});
$session->delete();

my $cookie = $q->cookie(jadrn000SID => '');

print $q->header( -cookie=>$cookie );


print <<END

<html>
<head>

</head>
<body>
<h2>You are logged out<h2>
</body>
</html>

END
