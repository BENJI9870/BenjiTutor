fetch('/api/question_list', {
    method: 'GET',
    
})
.then(response => response.json()) // parses response to JSON object which js can use
.then(data => {
    const template = document.getElementById('preview-template');

    for (let i = 0; i < data.length; i++) {
        const question = data[i];
        const clone = template.cloneNode(true);


        clone.querySelector('[template-item="title"]').innerText = question.title;
        clone.querySelector('[template-item="title"]').href = '/question/' + question.id;
        clone.querySelector('[template-item="username"]').innerText = question.username;
        clone.querySelector('[template-item="datetime"]').innerText = question.datetime;
        clone.querySelector('[template-item="main_text"]').innerText = question.mainText;
        clone.querySelector('[template-item="like-count"]').innerText = question.likesCount;
        clone.querySelector('[template-item="subject"]').innerText = question.subject;

        const likeBtn = clone.getElementsByTagName('button')[0];
        likeBtn.addEventListener('click', function() {
            likeQuestion(question.id, clone.querySelector('[template-item="like-count"]'));
        })

        document.getElementById('list-container').appendChild(clone);


    }})





    function likeQuestion(questionId, likeNode) {

    
        fetch('/api/like_question', {
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
