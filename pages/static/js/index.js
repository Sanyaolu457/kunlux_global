const searchContainer = document.getElementById('searchContainer');
const searchIcon = document.getElementById('searchIcon');

searchIcon.addEventListener('click', () => {
    searchContainer.classList.toggle('active');
    if(searchContainer.classList.contains('active')){
        searchContainer.querySelector('input').focus();
    }
});
