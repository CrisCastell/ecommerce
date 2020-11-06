
(function(window){
    const carousel = document.querySelector('#carousel-slide');
    const images = carousel.querySelectorAll('div');

    const prevBtn = document.querySelector('#prevBtn');
    const nextBtn = document.querySelector('#nextBtn');

    const time = 5000;
    let counter = 1;
    let size = images[0].clientWidth;
    carousel.style.transform = `translateX(${-size * counter}px)`;

    window.addEventListener('resize', ()=>{
        size = images[0].clientWidth;
        carousel.style.transition = 'none';
        counter = 1;
        carousel.style.transform = `translateX(${-size * counter}px)`;
    })

    let interval = setInterval(function(){
        printFunc(this)
    }, time);


    nextBtn.addEventListener('click', function(){
        if(counter >= images.length - 1) return
        clearInterval(interval)
        interval = setInterval(function(){
            printFunc(this)
        }, time);
        printFunc(this)
    })

    prevBtn.addEventListener('click', function(){
        if(counter <= 0) return
        clearInterval(interval)
        interval = setInterval(function(){
            printFunc(this)
        }, time);
        printFunc(this)
    })




    function printFunc(trigger){
        
        carousel.style.transition = 'transform 400ms ease-in-out';
        
        
        if(trigger.id === 'prevBtn'){
            counter--;
        }
        else{
            counter ++;
        }
        carousel.style.transform = `translateX(${-size * counter}px)`;
    }

    carousel.addEventListener('transitionend', ()=>{
        if(images[counter].id === 'firstImg'){
            carousel.style.transition = 'none';
            counter = images.length - counter;    
        }
        if(images[counter].id === 'lastImg'){
            carousel.style.transition = 'none';
            counter = images.length - 2; 
        }
        carousel.style.transform = `translateX(${-size * counter}px)`;
    })
})(window);