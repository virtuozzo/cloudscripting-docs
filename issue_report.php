<?php
    $token = "803fafa87b3a130c8f26d5f85f89a21db0d5fa1d";
    $url = "https://api.github.com/repos/dzotic9/docs/issues?access_token=" .$token;
    $selectedText = $_GET['selected'];
    $userName = $_GET['userName'];
    $comment = $_GET['comment'];
    $labels = "cs-bug-report";
    $page = $_GET['page'];
    $assignee = "dzotic9";
    $title = "CS-issue";

    $text = "Target page: " .$page.
        "<br>Name: " .$userName.
        "<br>Selected text: " .$selectedText.
        "<br>Comment: " .$comment;

    $data = '{"title": "'. $title .'", "body": "'. $text .'", "assignee": "'. $assignee .'", "labels": ["'. $labels .'"]}';
    $options = [
        'http' => array(
            'method'  => 'POST',
            'header'  => array(
                'User-Agent: PHP',
                'Content-type: application/x-www-form-urlencoded'
            ),
            'content' => $data
        ),
        'ssl' => array(
            'verify_peer'      => false,
            'verify_peer_name' => false
        )
    ];

    $context  = stream_context_create($options);
    $result = file_get_contents($url, FALSE, $context);
    var_dump($result);

    if ($result === FALSE) { exit("error"); }
    exit(0);
?>