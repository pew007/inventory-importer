#!/usr/bin/perl

use Crypt::SaltedHash;

my ($user, $password, $OK, $stored_user, $stored_pass, $line);
my @file_lines;

open INFILE, "<passwords.dat" or die "Cannot open file";
@file_lines = <INFILE>;
close INFILE;

print "Enter your username: ";
$user = <STDIN>;
chomp $user;
print "Enter your password: ";
$password = <STDIN>;
chomp $password;

$OK = 0;

foreach $line (@file_lines) {
    chomp $line;
    ($stored_user, $stored_pass) = split /=/, $line;

    if ($stored_user eq $user &&
        Crypt::SaltedHash->validate($stored_pass, $password)) {
        $OK = 1;
        last;
    }
}

if ($OK) {
    print "OK, you are authorized.\n";
}
else {
    print "ERROR: unauthorized user.\n";
}
