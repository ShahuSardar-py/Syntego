<?php
require_once 'functions.php';
session_start();
$message = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (isset($_POST['unsubscribe_email'])) {
        $email = $_POST['unsubscribe_email'];
        $code = generateVerificationCode();

        if (!file_exists(__DIR__ . '/verification_codes')) {
            mkdir(__DIR__ . '/verification_codes', 0777, true);
        }

        file_put_contents(__DIR__ . "/verification_codes/{$email}.txt", $code);

        $subject = "Confirm Un-subscription";
        $body = "<p>To confirm un-subscription, use this code: <strong>$code</strong></p>";
        $headers = "MIME-Version: 1.0\r\nContent-type:text/html;charset=UTF-8\r\nFrom: no-reply@example.com";
        mail($email, $subject, $body, $headers);

        $_SESSION['unsubscribe_email'] = $email;
        $message = "Unsubscription code sent to $email.";
    } elseif (isset($_POST['verification_code'])) {
        $email = $_SESSION['unsubscribe_email'] ?? null;
        $code = $_POST['verification_code'];

        if ($email && verifyCode($email, $code)) {
            unsubscribeEmail($email);
            unlink(__DIR__ . "/verification_codes/{$email}.txt");
            unset($_SESSION['unsubscribe_email']);
            $message = "You have been unsubscribed.";
        } else {
            $message = "Unsubscription verification failed.";
        }
    }
}
?>
<!DOCTYPE html>
<html>
<head><title>Unsubscribe</title></head>
<body>
<h2>Unsubscribe from XKCD Comics</h2>
<p><?php echo $message; ?></p>
<form method="POST">
    <input type="email" name="unsubscribe_email" required>
    <button id="submit-unsubscribe">Unsubscribe</button>
</form>
<form method="POST">
    <input type="text" name="verification_code" maxlength="6" required>
    <button id="submit-verification">Verify</button>
</form>
</body>
</html>
