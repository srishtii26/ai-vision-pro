function animateCounter(id, target, suffix = "") {
    let count = 0;
    const element = document.getElementById(id);

    const interval = setInterval(() => {

        count += Math.ceil(target / 100);

        if(count >= target){
            count = target;
            clearInterval(interval);
        }

        element.innerText = count + suffix;

    },20);
}

window.onload = () => {
    animateCounter("imagesCount", 1250, "+");
    animateCounter("predictionsCount", 3400, "+");
    animateCounter("accuracyCount", 89, "%");
};