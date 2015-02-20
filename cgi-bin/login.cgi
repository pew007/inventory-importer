#!/usr/bin/perl

use CGI;
use CGI::Session;
use CGI::Carp qw (fatalsToBrowser);
use Crypt::SaltedHash;
use strict;
use warnings;

my $cgi = new CGI;

open (LOG, ">/vagrant/logs/log");

if (authenticate_user()) {
    send_to_main();
} else {
    send_to_login_error();
}

sub authenticate_user {
    my $username = $cgi->param("username");
    my $password = $cgi->param("password");

    open DATA, "</vagrant/cgi-bin/passwords.dat" or die "Cannot open file";
    my @file_lines = <DATA>;
    close DATA;

    my $user_authenticated = 0;
    my $line;
    my ($stored_user, $stored_pass);

    foreach $line (@file_lines) {
        chomp $line;
        ($stored_user, $stored_pass) = split /=/, $line;

        if ($stored_user eq $username && Crypt::SaltedHash->validate($stored_pass, $password)) {
            $user_authenticated = 1;
            return $user_authenticated;
        }
    }

    return $user_authenticated;
}

sub send_to_login_error {
    print "Content-type: text/html\n\n";
    print <<END;

<html>
<head>
    <meta http-equiv="refresh" content="0; url=http://localhost:8081/error.html">
</head>
<body></body>
</html>

END
}

sub send_to_main {
    my $token   = $cgi->param("token");
    my $sid     = $cgi->cookie("jadrn048SID") || undef;
    my $session = new CGI::Session(undef, $sid, {Directory=>'/tmp'});
    my $cookie  = $cgi->cookie(jadrn048SID => $session->id);
    my $previous_token = $session->param('token');

    $session->param('token', $token);
    $session->expires('+1d');

    print $cgi->header(
        '-cookie' => $cookie
        );

    print "session id is " . $session->id() . "<br>";
    print "session id from cookie is $sid<br>";
    print "previous_token is $previous_token<br>";
    print "token from POST is $token<br>";
    print "token from session is " . $session->param('token') . "<br>";

    print <<END

<html>
<head></head>
<body>
Private page <br><br>
<a href="/cgi-bin/logout.cgi">Logout Now</a>
</body>

END
}
