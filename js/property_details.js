    const heroGridImages = document.querySelector('.hero-grid-images');
    const images = heroGridImages.querySelectorAll('img');
    const heroThumbnails = document.querySelector('.hero-thumbnails');

    // Function to get the value of a CSS variable
    function getCssVariableValue(variable) {
        return getComputedStyle(document.documentElement).getPropertyValue(variable).trim();
    }

    // Read the --max-thumbnails variable
    const maxThumbnails = parseInt(getCssVariableValue('--max-thumbnails'), 10);

    images.forEach((image, index) => {
        if (index < maxThumbnails) {
            //const thumbnail = document.createElement('img');
            const thumbnailContainer = document.createElement('div');                        

            heroThumbnails.appendChild(thumbnailContainer);

            if((index+1) !== maxThumbnails) {                
                thumbnailContainer.innerHTML = `<img src="${image.src}" alt="Thumbnail ${index + 1}">`;
            } else {                
                thumbnailContainer.innerHTML = `
                    <img src="${image.src}" alt="Thumbnail ${index + 1}">
                    <form id="frm_show_more">
                        <a href="#" class="show-more-link" title="show more"                            
                            mix-get="/property/show-more"
                        >show more</a>    
                    </form>
                `;
            }
        }        
    });

    

    // Following code is for booking section slide up for mobile version.
    const showSlideUp = document.querySelector(".show-slide-up");

    const closeSlideUp = document.querySelector(".close-slide-up");

    const slideUpDiv = document.querySelector('.slide-up-div');

    showSlideUp.addEventListener("click", function() {
        toggleSlideUpDiv();
    });

    closeSlideUp.addEventListener("click", function() {
        toggleSlideUpDiv();
    });

    function toggleSlideUpDiv() 
    {
        slideUpDiv.classList.toggle('active');
        slideUpDiv.classList.remove('hide-aside');
    }

    function checkViewportWidth() {
        
        if (window.innerWidth > 640) {
            slideUpDiv.classList.remove('slide-up-div');
        } else {
            slideUpDiv.classList.add('slide-up-div');
        }
    }

    checkViewportWidth();
    
    window.addEventListener('resize', checkViewportWidth);

    function resetForm()
    {
        const form = document.querySelector("#frm_book");
        form.reset();        
    }