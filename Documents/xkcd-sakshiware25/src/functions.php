<?php
function generateVerificationCode() {
    return str_pad(random_int(0, 999999), 6, '0', STR_PAD_LEFT);
}

function registerEmail($email) {
    $file = __DIR__ . '/registered_emails.txt';
    $emails = file($file, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
    if (!in_array($email, $emails)) {
        file_put_contents($file, $email . PHP_EOL, FILE_APPEND);
    }
}

function unsubscribeEmail($email) {
    $file = __DIR__ . '/registered_emails.txt';
    $emails = file($file, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
    $updated = array_filter($emails, fn($e) => trim($e) !== trim($email));
    file_put_contents($file, implode(PHP_EOL, $updated) . PHP_EOL);
}

function sendVerificationEmail($email, $code) {
    $subject = "Your Verification Code";
    $message = "<p>Your verification code is: <strong>$code</strong></p>";
    $headers = "MIME-Version: 1.0\r\nContent-type:text/html;charset=UTF-8\r\nFrom: no-reply@example.com";
    mail($email, $subject, $message, $headers);
    $_SESSION[$email] = $code;
}

function verifyCode($email, $code) {
    $sessionFile = __DIR__ . "/verification_codes/{$email}.txt";
    return file_exists($sessionFile) && trim(file_get_contents($sessionFile)) === $code;
}

function fetchAndFormatXKCDData() {
    $randomId = rand(1, 3000);
    $url = "https://xkcd.com/$randomId/info.0.json";
    $json = file_get_contents($url);
    $data = json_decode($json, true);
    return "<h2>XKCD Comic</h2>
            <img src=\"{$data['img']}\" alt=\"XKCD Comic\">
            <p><a href='https://example.com/src/unsubscribe.php' id='unsubscribe-button'>Unsubscribe</a></p>";
}

function sendXKCDUpdatesToSubscribers() {
    $file = __DIR__ . '/registered_emails.txt';
    $emails = file($file, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
    $htmlContent = fetchAndFormatXKCDData();
    $subject = "Your XKCD Comic";
    $headers = "MIME-Version: 1.0\r\nContent-type:text/html;charset=UTF-8\r\nFrom: no-reply@example.com";
    foreach ($emails as $email) {
        mail($email, $subject, $htmlContent, $headers);
    }
}
