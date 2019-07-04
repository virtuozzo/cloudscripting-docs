<?php
    $token = "3d8cdb66cbbef202194e6307aebb9d596df2ce95";
    $url = "https://api.github.com/repos/dzotic9/docs/issues";
    $selectedText = $_POST['selected'];
    $userName = $_POST['userName'];
    $context = $_POST['context'];
    $comment = $_POST['comment'];
    $labels = "cs-bug-report";
    $page = $_POST['page'];
    $assignee = "dzotic9";

    function checkRequiredParams($params) {
        foreach ($params as $key => $value) {
            if (empty($value)) {
                exit("Parameter " . $key . " is required");
            }
        }
    }

    function wr_log($log_msg) {
        $log_filepath = "log/";
        if (!file_exists($log_filepath))
        {
            // create directory/folder uploads.
            mkdir($log_filepath, 0777, true);
        }
        $log_file_data = $log_filepath.'/GitHub_issue_log_' . date('d-M-Y') . '.log';
        file_put_contents($log_file_data, $log_msg . "\nEND\n\n", FILE_APPEND);
    }

    function sendRequest($URL, $BODY, $TOKEN) {
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $URL);
        curl_setopt($ch, CURLOPT_POST, 1);
        curl_setopt($ch, CURLOPT_POSTFIELDS, $BODY);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER, array(
            'User-Agent: PHP',
            'Authorization: token '.$TOKEN
        ));
        $resp = curl_exec($ch);
        curl_close ($ch);
        return $resp;
    }

    checkRequiredParams(array('page' => $page, 'comment' => $comment));

    if (isset($selectedText)) {
        $firstWords = strtok($selectedText, ' ').' '.strtok(' ').' '.strtok(' ');

        if (strlen($selectedText) != strlen(trim($firstWords))) {
            $firstWords  = substr($firstWords, 0, 30)."...";
        }
    }

    if (isset($comment)) {
        $tmpComment = strtok($comment, ' ').' '.strtok(' ').' '.strtok(' ');

        if (strlen($comment) != strlen(trim($tmpComment))) {
            $firstWords .= ' - '.substr(strtok($comment, ' ').' '.strtok(' ').' '.strtok(' '), 0, 30)."...";
        } else {
            $firstWords .= ' - '.$comment;
        }
    }

    $title = "[${page}:${userName}]: ${firstWords}";
    $title = str_replace("\n","\\n", $title);
    $title = str_replace("\"","\\\"", $title);

    $selectedText = trim($selectedText);
    $text = "## Target page:\\r\\n" . "[http://".$_SERVER['HTTP_HOST'].$page."](http://" . $_SERVER['HTTP_HOST'] .$page.")\\n".
        "## Reporter:\\r\\n" .$userName."\\n".
        "## Comment:\\r\\n" .$comment."\\r\\n".
        "## Selected text:\\r\\n" . $context."\\r\\n";

    $text = str_replace("\n","\\n",$text);
    $text = str_replace("\"","\\\"",$text);
    $data = '{"title": "'. $title .'", "body": "'. $text .'", "assignee": "'. $assignee .'", "labels": ["'. $labels .'"]}';

    $server_output = sendRequest($url, $data, $token);
    $data=json_decode($server_output ,true);
    wr_log($server_output);

    if (!empty($data['id'])) {
        print_r("The issue on GitHub successfully created with id - " . $data['id']);
    } else {
        print_r("Some error is occuer:" .$server_output);
    }
    exit();
?>