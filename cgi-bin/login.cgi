#!/usr/bin/perl

use CGI;
use CGI::Session;
use CGI::Carp qw (fatalsToBrowser);
use Crypt::SaltedHash;
use strict;
use warnings;

my $q;
if (authenticate_user()) {
    send_to_main();
} else {
    send_to_login_error();
}

sub authenticate_user {
    $q = new CGI;
    my $username = $q->param("username");
    my $password = $q->param("password");
    open DATA, "</cgi-bin/password.dat" or die "Cannot open file";
    @file_lines = <DATA>;
    close DATA;

    $user_authenticated = 0;

    foreach $line (@file_lines) {
        chomp $line;
        ($stored_user, $stored_pass) = split /=/, $line;
        if ($stored_user eq $user && Crypt::SaltedHash->validate($stored_pass, $password)) {
            $user_authenticated = 1;
            last;
        }

        return $user_authenticated;
    }
}

sub send_to_login_error {
    print <<END;

Content-type: text/html


<html>
<head>
    <meta http-equiv="refresh" content="0; url=http://localhost:8081/error.html">
</head>
<body></body>
</html>

END
}

sub send_to_main {
    my $session = new CGI::Session(undef, undef, {Directory=>'/tmp'});
    $session->expires('+1d');
    my $cookie = $q->cookie(jadrn000SID => $session->id);
    print $q->header( -cookie=>$cookie);


    print <<END

<html>
<head></head>
<body>
Private page
<a href="/cgi-bin/logout.cgi">Logout Now</a>
</body>

END
}
