#!/usr/bin/perl

use Crypt::SaltedHash;

my @users = ('cs645', 'pwang', 'pew007', 'jadrn000');
my @passwords = ('sp2015', 'wangpengyu', 'Wpy@0407', 'cs645');
my @encrypted_passwords;
my $arr_len = @users;

for ($i = 0; $i < $arr_len; $i++) {
    my $encryption_object = Crypt::SaltedHash->new(algorithm => 'SHA-2');
    $encryption_object->add($passwords[$i]);
    push(@encrypted_passwords, $encryption_object->generate);
}

open(DATA, ">passwords.dat") or die "Cannot open file";

for ($i = 0; $i < $arr_len; $i++) {
    print DATA $users[$i]."=".$encrypted_passwords[$i]."\n";
}

close(DATA)
