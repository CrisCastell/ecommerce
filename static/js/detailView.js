(function(){
console.log('sirve')
const secImages = document.querySelectorAll('.secondary-img');
const mainImg = document.querySelector('#main-img');
const slide = document.querySelector('#other-slideh');


secImages.forEach(img => {
    img.addEventListener('click', function(){
        mainImg.setAttribute('src', img.src)
    })
})
})();