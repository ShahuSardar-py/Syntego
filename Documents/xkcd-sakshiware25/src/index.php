<?php
require_once 'functions.php';
session_start();
$message = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (isset($_POST['email'])) {
        $email = $_POST['email'];
        $code = generateVerificationCode();

        if (!file_exists(__DIR__ . '/verification_codes')) {
            mkdir(__DIR__ . '/verification_codes', 0777, true);
        }

        file_put_contents(__DIR__ . "/verification_codes/{$email}.txt", $code);
        sendVerificationEmail($email, $code);
        $_SESSION[$email] = $code;
        $message = "Verification code sent to $email";

    } elseif (isset($_POST['verification_code'])) {
        $email = array_keys($_SESSION)[0] ?? null;
        $code = $_POST['verification_code'];

        if ($email && verifyCode($email, $code)) {
            registerEmail($email);
            unlink(__DIR__ . "/verification_codes/{$email}.txt");
            $message = "Email $email successfully registered!";
        } else {
            $message = "Verification failed.";
        }
    }
}
?>
<!DOCTYPE html>
<html>
<head><title>XKCD Subscription</title></head>
<body>
<h2>Subscribe to XKCD Comics</h2>
<p><?php echo $message; ?></p>
<form method="POST">
    <input type="email" name="email" required>
    <button id="submit-email">Submit</button>
</form>
<form method="POST">
    <input type="text" name="verification_code" maxlength="6" required>
    <button id="submit-verification">Verify</button>
</form>
</body>
</html>
