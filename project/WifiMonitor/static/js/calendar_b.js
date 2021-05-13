const date_b = new Date();

const renderCalendar_b = () => {
    date_b.setDate(1);

    const monthDays = document.querySelector('.days-b');
    const lastDay = new Date(date_b.getFullYear(), date_b.getMonth()+1, 0).getDate();
    const prevLastDay = new Date(date_b.getFullYear(), date_b.getMonth(), 0).getDate();
    const firstDayIndex = date_b.getDay();
    const lastDayIndex = new Date(date_b.getFullYear(), date_b.getMonth()+1, 0).getDay();
    const nextDays = 7 - lastDayIndex - 1;
    const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September",
                   "October", "November", "December"];

    document.querySelector('.date-b h5').innerHTML = months[date_b.getMonth()];
    document.querySelector('.date-b p').innerHTML = new Date().toDateString();

    let days = "";
    for(let x = firstDayIndex; x > 0; x--){
        days += `<div class="prev-date">${prevLastDay - x + 1}</div>`
    }

    for (let i = 1; i <= lastDay; i++){
        if(i === new Date().getDate() && date_b.getMonth() === new Date().getMonth()){
            days += `<div class="today">${i}</div>`;
        } else {
            days += `<div>${i}</div>`;
        }
    }

    for(let j = 1; j <= nextDays; j++){
        days += `<div class="next-date">${j}</div>`;
        monthDays.innerHTML = days;
    }
}

document.querySelector('.prev-b').addEventListener('click', () => {
    date_b.setMonth(date_b.getMonth() - 1);
    renderCalendar_b();
});

document.querySelector('.next-b').addEventListener('click', () => {
    date_b.setMonth(date_b.getMonth() + 1);
    renderCalendar_b();
});

renderCalendar_b();