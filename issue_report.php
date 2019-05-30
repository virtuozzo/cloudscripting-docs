<?php
    $token = "3d8cdb66cbbef202194e6307aebb9d596df2ce95";
    $url = "https://api.github.com/repos/dzotic9/docs/issues";
    $selectedText = $_POST['selected'];
    $userName = $_POST['userName'];
    $parent = $_POST['parent'];
    $comment = $_POST['comment'];
    $labels = "cs-bug-report";
    $page = $_POST['page'];
    $assignee = "dzotic9";

    if (isset($selectedText)) {
        $firstWords = strtok($selectedText, ' ').' '.strtok(' ').' '.strtok(' ');
        $firstWords = substr($firstWords, 0, 30);
    }

    if (isset($comment)) {
        $firstWords .= ' - '.substr(strtok($comment, ' ').' '.strtok(' ').' '.strtok(' '), 0, 30);
    }

    $title = "[${page}:${userName}]: ${firstWords}";
    $title = str_replace("\n","\\n", $title);
    $title = str_replace("\"","\\\"", $title);
    $parent = str_replace("`", "", $parent);

    $selectedText = trim($selectedText);
    $text = "## Target page:\\r\\n" .$page."\\n".
        "## Name:\\r\\n" .$userName."\\n".
        "## Comment:\\r\\n" .$comment."\\r\\n".
        "## Selected text:\\r\\n" . str_replace($selectedText, "\\r\\n```\\r\\n" . $selectedText . "\\r\\n```\\r\\n", $parent)."\\r\\n";

    $text = str_replace("\n","\\n",$text);
$text = str_replace("\"","\\\"",$text);
    $data = '{"title": "'. $title .'", "body": "'. $text .'", "assignee": "'. $assignee .'", "labels": ["'. $labels .'"]}'; #addslashes

    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, array(
        'User-Agent: PHP',
        'Authorization: token '.$token
    ));
    $server_output = curl_exec($ch);
    curl_close ($ch);
    print_r($server_output)
?>