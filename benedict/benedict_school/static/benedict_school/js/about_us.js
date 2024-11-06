document.addEventListener('DOMContentLoaded', function() {
    // Your code here
});

function openModal(member) {
    const modal = document.getElementById('team-modal');
    const modalContent = document.getElementById('modal-content');
    modalContent.innerHTML = `
        <h2>${member.name}</h2>
        <p>${member.bio}</p>
        <button onclick="closeModal()">Close</button>
    `;
    modal.style.display = 'block';
}

function closeModal() {
    const modal = document.getElementById('team-modal');
    modal.style.display = 'none';
}

const teamMembers = document.querySelectorAll('.team-member');
teamMembers.forEach(member => {
    member.addEventListener('click', function() {
        const memberData = {
            name: this.querySelector('h3').innerText,
            bio: this.querySelector('p').innerText,
        };
        openModal(memberData);
    });
});

document.addEventListener('DOMContentLoaded', function() {
    // Initialize modals or any interactive components
});

// JavaScript function to toggle anthem visibility
function toggleAnthem() {
    const anthemContent = document.getElementById("anthemContent");
    if (anthemContent.style.display === "none") {
        anthemContent.style.display = "block";
    } else {
        anthemContent.style.display = "none";
    }
}

