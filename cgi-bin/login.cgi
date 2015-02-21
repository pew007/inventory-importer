#!/usr/bin/perl

use CGI;
use CGI::Session;
use CGI::Carp qw (fatalsToBrowser);
use Crypt::SaltedHash;
use Session::Token;
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

    # Retrive session from cookie or create a new one
    my $cookie_sid = $cgi->cookie('jadrn048SID') || undef;
    my $session = new CGI::Session(undef, $cookie_sid, {Directory=>'/tmp'});

    my $token = Session::Token->new->get;

    # Set cookie
    print $cgi->header(
        '-cookie'        => $cgi->cookie(jadrn048SID => $session->id),
        '-Cache-Control' => 'no-cache, no-store, must-revalidate, max-age=0'
        );

    # Initial login
    if ($cookie_sid == undef) {
        # Create security token and store in session
        $session->param('token', $token);
        $session->expires('+1d');

        print "new log in<br><br>";
        print "token from session is " . $session->param('token') . "<br>";
        print "<a href='/cgi-bin/logout.cgi'>Logout Now</a>";
        return;
    }

    # Validate existing session
    if ($cookie_sid eq $session->id && $token eq $session->param('token')) {
        print "sid from cookie is $cookie_sid<br><br>";
        print "token from session is " . $session->param('token') . "<br>";
        print "new token is $token<br><br>";
        print <<END

<html>
<head></head>
<body>

Private page <br><br>
<a href="/cgi-bin/logout.cgi">Logout Now</a>
</body>

END
    } else {
        print "sid from cookie is $cookie_sid<br><br>";
        print "session id is " . $session->id . "<br><br>";
        print "token from session is " . $session->param('token') . "<br>";
        print "new token is $token<br><br>";
        print "invalid session. please log in again";
    }
}
