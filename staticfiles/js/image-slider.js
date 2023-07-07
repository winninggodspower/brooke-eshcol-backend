const img  = $('#hero-img');
const headingText  = $('#hero-heading');
const heroPtext  = $('#hero-ptext');

let animating = false
let screenWidth = window.outerWidth


const headingItems = [
    {
        img : img.attr("src"),
        headingText : headingText.text(),
        pText: heroPtext.text(),
        left: '0%',
    },
    {
        img : "../static/assets/img/tablet.png",
        headingText : "Let us help you acquire the right digital skills that are in global demand. ",
        pText: "we have  trained professionals with competent IT skills and knowledge. ",
        left: '0%',
    },
    {
        img : "../static/assets/img/hero-img3.png",
        headingText : "Get project-based learning benefit, examples and resources",
        pText: "Create shareable  projects as you learn.",
        left: '50%',
    },

]

const ChangeHeroSection = (element)=>{
    let id = element.attr('id')[element.attr('id').length - 1]
    id = new Number(id)

    let currentHeadingItem = headingItems[id - 1]
    

    // fading the elements to be changed out and;
    //changing element content
    //fadein the element that has been change
    img.fadeOut(()=>{
        img.attr('src', currentHeadingItem.img)
        $('.hero-img').css('left', currentHeadingItem.left)
        img.fadeIn(1500)
    })
    headingText.fadeOut(()=>{
        headingText.text(currentHeadingItem.headingText)
        headingText.fadeIn(1500)
    })
    heroPtext.fadeOut(()=>{
        heroPtext.text(currentHeadingItem.pText)
        heroPtext.fadeIn(1500, ()=>{
            animating = false
        })
    })

}

// click event listener to fire the FadeTransition
$('.circle-nav').click((e)=>{
    if (animating){
        return
    }
    const clickedCircle = $(e.currentTarget)
    HandleHeadingFadeTransition(clickedCircle)
})


// function that starts the fade transition
const HandleHeadingFadeTransition = (clickedCircle)=>{
    animating = true

    // changing active icon to the one clicked
    $('.circle-nav').css('background', '#A0071694')
    clickedCircle.css('background', 'var(--danger)')

    ChangeHeroSection(clickedCircle)
}

// firing the fade transition function on intervals
const transitionDelayTime = 15000
let circleNavId = 1;
setInterval(() => {
    if (circleNavId <= 2) {
        circleNavId ++
    }else{
        circleNavId = 1;
    }

    if (animating){
        return
    }

    HandleHeadingFadeTransition($(`#circle-nav${circleNavId}`))
}, transitionDelayTime);
