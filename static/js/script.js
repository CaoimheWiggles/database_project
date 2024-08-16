/* poll */


document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById('poll-form');
    const resultsContainer = document.getElementById('poll-results');

    form.addEventListener('submit', function(event) {
        event.preventDefault(); 

        const selectedOption = form.elements['activity'].value; 

        fetch('/vote', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ choice: selectedOption })
        })
        .then(response => response.json())
        .then(data => {
            
            resultsContainer.innerHTML = '';

            const maxVotes = Math.max(...Object.values(data));

            Object.keys(data).forEach(activity => {
                const votes = data[activity] || 0;
                const resultBox = document.createElement('div');
                resultBox.classList.add('result-box');
                resultBox.dataset.votes = votes;

                const percentage = maxVotes ? (votes / maxVotes) * 100 : 0;
                resultBox.style.background = `linear-gradient(90deg, rgb(199, 140, 214) ${percentage}%, #ddd ${percentage}%)`;

                resultBox.textContent = `${activity}: ${votes} votes`;

                resultsContainer.appendChild(resultBox);
            });
        })
        .catch(error => console.error('Error:', error));
    });
});

/* scroll */

document.addEventListener('DOMContentLoaded', function () {
    const postSections = document.querySelectorAll('.post-content section');

    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            } else {
                entry.target.classList.remove('visible');
            }
        });
    });

    postSections.forEach(section => {
        observer.observe(section);
    });
});


/* li scroll */

document.addEventListener('DOMContentLoaded', function () {
    const listItems = document.querySelectorAll('.post-content section li');
    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            } else {
                entry.target.classList.remove('visible');
            }
        });
    }, {
        threshold: 0.1
    });

    listItems.forEach(item => {
        observer.observe(item);
    });
});



/* search */

document.addEventListener("DOMContentLoaded", function() {
    const searchInput = document.getElementById("search-input");
    const searchResults = document.getElementById("search-results");

    const allBlogPosts = [
        {"title": "How to Juggle Being a Working Mother During the Summer Holidays", "url": "/featured"},
        {"title": "What It Means to Be Emotionally Available to Kids", "url": "/post1"},
        {"title": "Navigating The 'Terrible Twos': Finding Happiness Amidst the Chaos", "url": "/post2"},
        {"title": "Dealing With Picky Eaters", "url": "/post3"},
        {"title": "Single Parent Triumph: Overcoming with Courage", "url": "/post4"},
        {"title": "Navigating Screen Time", "url": "/post5"},
        {"title": "Parenting Through The Teenage Years", "url": "/post6"}
    ];

    searchInput.addEventListener("input", function() {
        const keyword = searchInput.value.trim().toLowerCase();
        if (keyword === "") {
            clearSearchSuggestions();
        } else {
            const filteredPosts = allBlogPosts.filter(post => post.title.toLowerCase().includes(keyword));
            displaySearchSuggestions(filteredPosts);
        }
    });

    function displaySearchSuggestions(suggestions) {
        searchResults.innerHTML = "";

        suggestions.forEach(post => {
            const link = document.createElement("a");
            link.textContent = post.title;
            link.href = post.url;
            link.classList.add("search-suggestion");
            const listItem = document.createElement("div");
            listItem.appendChild(link);
            searchResults.appendChild(listItem);
        });
    }

    function clearSearchSuggestions() {
        searchResults.innerHTML = "";
    }
});


/* thank you slider */


let slideIndex = 0;
showSlides(slideIndex);

function showSlides(index) {
    const slides = document.getElementsByClassName("blog-post2");
    if (index >= slides.length) { slideIndex = 0 }
    if (index < 0) { slideIndex = slides.length - 1 }
    for (let i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    slides[slideIndex].style.display = "block";
}

function prevSlide() {
    showSlides(slideIndex -= 1);
}

function nextSlide() {
    showSlides(slideIndex += 1);
}

document.addEventListener('keydown', function(event) {
    if (event.key === 'ArrowLeft') {
        prevSlide();
    } else if (event.key === 'ArrowRight') {
        nextSlide();
    }
});

document.addEventListener('wheel', function(event) {
    if (event.deltaY < 0) {
        prevSlide();
    } else if (event.deltaY > 0) {
        nextSlide();
    }
});


