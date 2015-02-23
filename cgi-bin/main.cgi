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
print $cgi->header;

render_main();

sub render_main {
    my $dbh = get_db_connection();

    # Get vendor list
    my $sth = $dbh->prepare("SELECT * FROM vendor");
    $sth->execute();
    my $vendors;
    push @{$vendors}, $_ while $_ = $sth->fetchrow_hashref();

    # Get category list
    my $sth = $dbh->prepare("SELECT * FROM category");
    $sth->execute();
    my $categories;
    push @{$categories}, $_ while $_ = $sth->fetchrow_hashref();

    # Get platform list
    my $sth = $dbh->prepare("SELECT * FROM platform");
    $sth->execute();
    my $platforms;
    push @{$platforms}, $_ while $_ = $sth->fetchrow_hashref();

    # instantiate the template and substitute the values
    my $template = HTML::Template->new(filename => '/vagrant/templates/main.tmpl');
    $template->param(
        VENDORS     => $vendors,
        CATEGORIES  => $categories,
        PLATFORMS   => $platforms
    );

    $sth->finish();
    $dbh->disconnect();

    print $template->output;
}

sub get_db_connection {
    # my $host = "opatija.sdsu.edu";
    my $host = '127.0.0.1';
    my $port = "3306";
    my $database = "jadrn048";
    # my $username = "jadrnxxx";
    my $username = 'root';
    my $password = "";
    my $database_source = "dbi:mysql:$database:$host:$port";

    my $dbh = DBI->connect($database_source, $username, $password)
    or die 'Cannot connect to db';

    return $dbh;
}
