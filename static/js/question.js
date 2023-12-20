function likeQuestion() {

    
    fetch('/api/like_question', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            question_id: document.getElementById('question-id').value
        }) // body data type must match "Content-Type" header
    })
    .then(response => response.json()) // parses response to JSON object which js can use
    .then(data => {
        const likeNode = document.getElementById('question-like-count'); 
        if (data.success && data.action == 'like') {
            let likeCount = likeNode.innerText;
            // cast to int
            likeCount = parseInt(likeCount);
            likeCount += 1;
            likeNode.innerText = likeCount;
            
        } else if (data.success && data.action == 'unlike') {
            let likeCount = likeNode.innerText;

            console.log(likeCount)
            // cast to int
            likeCount = parseInt(likeCount);

            likeCount -= 1;
            likeNode.innerText = likeCount;
        } else {
            console.error(data.message)
        }
        }

    )
}


document.getElementById('question-like-btn').addEventListener('click', likeQuestion);

function comment(){
    const commentText = document.getElementById('comment_text').value;
    const questionId = document.getElementById('question-id').value;

    fetch('/api/new_comment', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            question_id: questionId,
            comment_text: commentText
        }) // body data type must match "Content-Type" header
    })
    .then(response => response.json()) // parses response to JSON object which js can use
    .then(data => {
        if (data.success) {
            window.location.reload();
        }

})}

document.getElementById('comment-submit-btn').addEventListener('click', comment);

function commentList(){
    fetch('/api/get_comments', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            question_id: document.getElementById('question-id').value
        }) // body data type must match "Content-Type" header
    })
    .then(response => response.json()) // parses response to JSON object which js can use
    .then(data => {
            const commentList = document.getElementById('comments-list');
            for (let comment of data) {
                console.log(comment);
                const clone = document.getElementById('comment-template').cloneNode(true);
                clone.querySelector('[comment-template="username"]').innerText = comment.username;
                clone.querySelector('[comment-template="datetime"]').innerText = comment.datetime;
                clone.querySelector('[comment-template="comment_text"]').innerText = comment.mainText;
                clone.querySelector('[comment-template="like-count"]').innerText = comment.likesCount;
                
                const likeBtn = clone.getElementsByTagName('button')[0];
                likeBtn.addEventListener('click', function() {
                    likeComment(comment.id, clone.querySelector('[comment-template="like-count"]'));
                })
                
                
                
                
                commentList.appendChild(clone);



            }

})}



function likeComment(commentId, likeNode) {

    
    fetch('/api/like_comment', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            comment_id: commentId
        }) // body data type must match "Content-Type" header
    })
    .then(response => response.json()) // parses response to JSON object which js can use
    .then(data => {
        if (data.success && data.action == 'like') {
            let likeCount = likeNode.innerText;
            // cast to int
            likeCount = parseInt(likeCount);
            console.log(likeCount)
            likeCount += 1;
            likeNode.innerText = likeCount;
            
        } else if (data.success && data.action == 'unlike') {
            let likeCount = likeNode.innerText;

            console.log(likeCount)
            // cast to int
            likeCount = parseInt(likeCount);

            likeCount -= 1;
            likeNode.innerText = likeCount;
        } else {
            console.error(data.message)
        }
        }

    )
}




function setBtnVisQuestion() {
    console.log('setBtnVisQuestion called');
    const questionId = document.getElementById('question-id').value;
    
    fetch('/api/is_logged_in', {
        method: 'GET'
    })
    .then(response => response.json()) // parses response to JSON object which js can use
    .then(data => {

        if (data.success) {
            const editBtn = document.getElementsByTagName('button')[2];
            editBtn.style.display = 'block'; // Ensure the button is visible
            
                // Your edit functionality here


            const deleteBtn = document.getElementsByTagName('button')[3];
            deleteBtn.style.display = 'block'; // Ensure the button is visible
            deleteBtn.addEventListener('click', function() {
                // Your delete functionality here
                deleteQuestion();
            });
        } else {
            console.log(document.getElementsByTagName('button'));
            document.getElementsByTagName('button')[2].style.display = 'none'; // Hide edit button
            document.getElementsByTagName('button')[3].style.display = 'none'; // Hide delete button
        }
    })}


function deleteQuestion() {
    const questionId = document.getElementById('question-id').value;
    
    fetch('/api/delete_question', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            question_id: questionId
        }) // body data type must match "Content-Type" header
    })
    .then(response => response.json()) // parses response to JSON object which js can use
    .then(data => {

        if (data.success) {
            window.location.href = '/question_list'; 
        } else {
            alert('Error deleting question: ' + data.message)
        }
    })}

    

setBtnVisQuestion();
commentList();