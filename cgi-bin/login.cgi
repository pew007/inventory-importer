#!/usr/bin/perl

use CGI;
use CGI::Session;
use CGI::Carp qw (fatalsToBrowser);
use Crypt::SaltedHash;
use DBI;
use Session::Token;
use HTML::Template;
use strict;
use warnings;

my $cgi = new CGI;

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
    print $cgi->redirect('http://localhost:8081/error.html');
}

sub send_to_main {
    # Retrive session from cookie or create a new one
    my $cookie_sid = $cgi->cookie('jadrn048SID') || undef;
    my $session = new CGI::Session(undef, $cookie_sid, {Directory=>'/tmp'});

    my $token = Session::Token->new->get;
    my $token_in_session = $session->param('token');

    # Set cookie
    # print $cgi->header('-cookie' => $cgi->cookie(jadrn048SID => $session->id));

    print $cgi->redirect('http://localhost:8081/cgi-bin/main.cgi');
}
