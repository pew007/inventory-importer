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

    my $vendors     = get_all('vendor');
    my $categories  = get_all('category');
    my $platforms   = get_all('platform');

    # instantiate the template and substitute the values
    my $template = HTML::Template->new(filename => '/vagrant/templates/main.tmpl');
    $template->param(
        VENDORS     => $vendors,
        CATEGORIES  => $categories,
        PLATFORMS   => $platforms
    );

    print $template->output;
}

sub get_all {
    my ($table) = @_;

    my $dbh = get_db_connection();
    my $sth = $dbh->prepare("SELECT * FROM $table");
    $sth->execute();
    my $results;
    push @{$results}, $_ while $_ = $sth->fetchrow_hashref();

    $sth->finish();
    $dbh->disconnect();

    return $results;
}

sub get_db_connection {
    # my $host = "opatija.sdsu.edu";
    my $host = '127.0.0.1';
    my $port = "3306";
    my $database = "jadrn048";
    # my $username = "jadrn048";
    my $username = 'root';
    my $password = "";
    my $database_source = "dbi:mysql:$database:$host:$port";

    my $dbh = DBI->connect($database_source, $username, $password)
    or die 'Cannot connect to db';

    return $dbh;
}
