#!/usr/bin/perl

#   This script reads a username and password from the command line,
#   then compares it to entries in password.dat.  You will want to use
#   this technique in your script that validates user logins.
#   CS645, Spring 2015
#   Alan Riggins

use Crypt::SaltedHash;


my ($user, $password, $OK, $stored_user, $stored_pass, $line);
my @file_lines;

open INFILE, "<passwords.dat" or die "Cannot open file.";
@file_lines = <INFILE>;
close INFILE;

print "Enter your username: ";
$user = <STDIN>;
chomp $user;
print "Enter your password: ";
$password = <STDIN>;
chomp $password;

$OK = 0; #not authorized

foreach $line (@file_lines) {
    chomp $line;
    ($stored_user, $stored_pass) = split /=/, $line; 
      
    if($stored_user eq $user && 
            Crypt::SaltedHash->validate($stored_pass, $password)) {
        $OK = 1;
        last;
        }           
    }
    
if($OK) {
    print "OK, you are authorized.\n";
    }
else {
    print "ERROR, unauthorized user.\n";
    }

    

