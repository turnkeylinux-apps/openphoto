<?php
# encrypt/decrypt string (assumes null salt)

define('PATH_LIBRARY', '/var/www/openphoto/src/libraries');
include PATH_LIBRARY . '/models/Utility.php';

if (count($argv)!=4) die("usage: $argv[0] <encrypt|decrypt> string secret\n");

$action = $argv[1];
$string = $argv[2];
$secret = $argv[3];
$utility = new Utility();

switch ($action) {
    case "encrypt":
        print $utility->encrypt($string, $secret, null);
        break;
    case "decrypt":
        print $utility->decrypt($string, $secret, null);
        break;
    default:
        die("supported actions: encrypt, decrypt");
        break;
}

?>

