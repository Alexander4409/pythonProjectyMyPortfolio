/*global gettext, pgettext, get_format, quickElement, removeChildren*/
/*
calendar.js - Calendar functions by Adrian Holovaty
depends on core.js for utility functions like removeChildren or quickElement
*/
'use strict';

{
    // CalendarNamespace -- Provides a collection of HTML calendar-related helper functions
    const CalendarNamespace = {
        monthsOfYear: [
            gettext('January'),
            gettext('February'),
            gettext('March'),
            gettext('April'),
            gettext('May'),
            gettext('June'),
            gettext('July'),
            gettext('August'),
            gettext('September'),
            gettext('October'),
            gettext('November'),
            gettext('December')
        ],
        monthsOfYearAbbrev: [
            pgettext('abbrev. month January', 'Jan'),
            pgettext('abbrev. month February', 'Feb'),
            pgettext('abbrev. month March', 'Mar'),
            pgettext('abbrev. month April', 'Apr'),
            pgettext('abbrev. month May', 'May'),
            pgettext('abbrev. month June', 'Jun'),
            pgettext('abbrev. month July', 'Jul'),
            pgettext('abbrev. month August', 'Aug'),
            pgettext('abbrev. month September', 'Sep'),
            pgettext('abbrev. month October', 'Oct'),
            pgettext('abbrev. month November', 'Nov'),
            pgettext('abbrev. month December', 'Dec')
        ],
        daysOfWeek: [
            pgettext('one letter Sunday', 'S'),
            pgettext('one letter Monday', 'M'),
            pgettext('one letter Tuesday', 'T'),
            pgettext('one letter Wednesday', 'W'),
            pgettext('one letter Thursday', 'T'),
            pgettext('one letter Friday', 'F'),
            pgettext('one letter Saturday', 'S')
        ],
        firstDayOfWeek: parseInt(get_format('FIRST_DAY_OF_WEEK')),
        isLeapYear: function (year) {
            return (((year % 4) === 0) && ((year % 100) !== 0) || ((year % 400) === 0));
        },
        getDaysInMonth: function (month, year) {
            let days;
            if (month === 1 || month === 3 || month === 5 || month === 7 || month === 8 || month === 10 || month === 12) {
                days = 31;
            }
            else if (month === 4 || month === 6 || month === 9 || month === 11) {
                days = 30;
            }
            else if (month === 2 && CalendarNamespace.isLeapYear(year)) {
                days = 29;
            }
            else {
                days = 28;
            }
            return days;
        },
        draw: function (month, year, div_id, callback, selected, bookedDates) {
            const today = new Date();
            const todayDay = today.getDate();
            const todayMonth = today.getMonth() + 1;
            const todayYear = today.getFullYear();
            let todayClass = '';

            let isSelectedMonth = false;
            if (typeof selected !== 'undefined') {
                isSelectedMonth = (selected.getUTCFullYear() === year && (selected.getUTCMonth() + 1) === month);
            }

            month = parseInt(month);
            year = parseInt(year);
            const calDiv = document.getElementById(div_id);
            removeChildren(calDiv);
            const calTable = document.createElement('table');
            quickElement('caption', calTable, CalendarNamespace.monthsOfYear[month - 1] + ' ' + year);
            const tableBody = quickElement('tbody', calTable);

            let tableRow = quickElement('tr', tableBody);
            for (let i = 0; i < 7; i++) {
                quickElement('th', tableRow, CalendarNamespace.daysOfWeek[(i + CalendarNamespace.firstDayOfWeek) % 7]);
            }

            const startingPos = new Date(year, month - 1, 1 - CalendarNamespace.firstDayOfWeek).getDay();
            const days = CalendarNamespace.getDaysInMonth(month, year);

            let nonDayCell;

            tableRow = quickElement('tr', tableBody);
            for (let i = 0; i < startingPos; i++) {
                nonDayCell = quickElement('td', tableRow, ' ');
                nonDayCell.className = "nonday";
            }

            function calendarMonth(y, m) {
                function onClick(e) {
                    e.preventDefault();
                    callback(y, m, this.textContent);
                }

                return onClick;
            }

            let currentDay = 1;
            for (let i = startingPos; currentDay <= days; i++) {
                if (i % 7 === 0 && currentDay !== 1) {
                    tableRow = quickElement('tr', tableBody);
                }
                if ((currentDay === todayDay) && (month === todayMonth) && (year === todayYear)) {
                    todayClass = 'today';
                } else {
                    todayClass = '';
                }

                if (isSelectedMonth && currentDay === selected.getUTCDate()) {
                    if (todayClass !== '') {
                        todayClass += " ";
                    }
                    todayClass += "selected";
                }

                const cell = quickElement('td', tableRow, '', 'class', todayClass);
                const link = quickElement('a', cell, currentDay, 'href', '#');
                link.addEventListener('click', calendarMonth(year, month));
                currentDay++;

                const currentDate = new Date(year, month - 1, currentDay - 1);
                const formattedDate = currentDate.toISOString().split('T')[0];
                if (bookedDates.includes(formattedDate)) {
                    cell.className += ' booked'; // добавляем класс для стилизации
                }

                // Задаем цвета для выбранных дат
                if (isSelectedMonth && selected.getUTCDate() === currentDay - 1) {
                    cell.style.backgroundColor = 'green'; // Задаем цвет фона для выбранной даты
                    cell.style.color = 'white'; // Задаем цвет текста для выбранной даты
                }
            }

            while (tableRow.childNodes.length < 7) {
                nonDayCell = quickElement('td', tableRow, ' ');
                nonDayCell.className = "nonday";
            }

            calDiv.appendChild(calTable);
        }
    };

    function Calendar(div_id, callback, selected, bookedDates) {
        this.div_id = div_id;
        this.callback = callback;
        this.today = new Date();
        this.currentMonth = this.today.getMonth() + 1;
        this.currentYear = this.today.getFullYear();
        if (typeof selected !== 'undefined') {
            this.selected = selected;
        }
        this.bookedDates = bookedDates || [];
        this.drawCurrent = function () {
            CalendarNamespace.draw(this.currentMonth, this.currentYear, this.div_id, this.callback, this.selected, this.bookedDates);
        };
        this.drawDate = function (month, year, selected) {
            this.currentMonth = month;
            this.currentYear = year;
            if (selected) {
                this.selected = selected;
            }
            this.drawCurrent();
        };
        this.drawPreviousMonth = function () {
            if (this.currentMonth === 1) {
                this.currentMonth = 12;
                this.currentYear--;
            }
            else {
                this.currentMonth--;
            }
            this.drawCurrent();
        };
        this.drawNextMonth = function () {
            if (this.currentMonth === 12) {
                this.currentMonth = 1;
                this.currentYear++;
            }
            else {
                this.currentMonth++;
            }
            this.drawCurrent();
        };
        this.drawPreviousYear = function () {
            this.currentYear--;
            this.drawCurrent();
        };
        this.drawNextYear = function () {
            this.currentYear++;
            this.drawCurrent();
        };
    }
    window.Calendar = Calendar;
    window.CalendarNamespace = CalendarNamespace;
}

document.addEventListener("DOMContentLoaded", function() {
    const bookedDates = "{{ booked_dates }}".split(','); // преобразуем строку в массив дат
    const calendar = new Calendar('calendar', null, null, bookedDates);
    const selectedDates = ['2023-11-26', '2023-11-29']; // ваши выбранные даты
    calendar.drawCurrent();
});
