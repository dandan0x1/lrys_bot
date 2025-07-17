// ==UserScript==
// @name         SpriteType 自动打字 + 自动 Tab 脚本
// @namespace    http://661100.xyz/
// @version      1.1
// @description  自动输入 SpriteType 单词并在结束后自动按下 Tab 进入下一轮，优化双 Tab 重启
// @author       DanDan的脚本
// @match        https://spritetype.irys.xyz/*
// @grant        none
// ==/UserScript==

(async function autoTypeSprite() {
    console.log("[SpriteType] 自动打字启动");

    function sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    function triggerInput(input, value) {
        const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
        const inputEvent = new Event('input', { bubbles: true });
        const keydownEvent = new KeyboardEvent('keydown', { key: value[value.length - 1], bubbles: true });
        const keyupEvent = new KeyboardEvent('keyup', { key: value[value.length - 1], bubbles: true });

        nativeInputValueSetter.call(input, value);
        input.dispatchEvent(inputEvent);
        input.dispatchEvent(keydownEvent);
        input.dispatchEvent(keyupEvent);
    }

    function clickElement(element) {
        if (element && !element.disabled) {
            try {
                element.dispatchEvent(new MouseEvent('mouseover', { bubbles: true, cancelable: true, view: window }));
                element.dispatchEvent(new MouseEvent('mousedown', { bubbles: true, cancelable: true, view: window }));
                element.dispatchEvent(new MouseEvent('mouseup', { bubbles: true, cancelable: true, view: window }));
                element.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true, view: window }));
                console.log(`✅ 点击元素: ${element.textContent.trim()}`);
                return true;
            } catch (e) {
                console.log(`❌ 点击失败: ${e.message}`);
                return false;
            }
        }
        return false;
    }

    function triggerSingleTab() {
        const el = document.activeElement;
        if (el) {
            el.dispatchEvent(new KeyboardEvent('keydown', {key: 'Tab', code: 'Tab', keyCode: 9, which: 9, bubbles: true}));
            el.dispatchEvent(new KeyboardEvent('keyup', {key: 'Tab', code: 'Tab', keyCode: 9, which: 9, bubbles: true}));
        }
    }

    function findButton(text) {
        const buttons = document.querySelectorAll('button');
        return Array.from(buttons).find(btn => btn.textContent.includes(text));
    }

    async function waitForInputFocusAndNewWord(maxAttempts = 10) {
        let attempts = 0;
        while (attempts < maxAttempts) {
            const input = document.querySelector('input[type="text"]');
            const wordElems = document.querySelectorAll('div[class*="text-"]');
            const activeWord = Array.from(wordElems).find(el =>
                el.innerText.trim().length > 0 &&
                window.getComputedStyle(el).color === 'rgb(255, 255, 255)'
            );

            if (input && document.activeElement === input && activeWord) {
                return true;
            }
            triggerSingleTab();
            await sleep(500);
            attempts++;
        }
        return false;
    }

    async function triggerDoubleTab() {
        console.log("🔄🔄 模拟双 Tab 键");
        triggerSingleTab();
        await sleep(100); // 两次 Tab 之间短暂延迟
        triggerSingleTab();
    }

    while (true) {
        const input = document.querySelector('input[type="text"]');
        if (!input) {
            await sleep(1000);
            continue;
        }

        input.focus();
        input.click();

        const submitButton = findButton('Submit to Leaderboard');
        if (submitButton) {
            while (!clickElement(submitButton)) await sleep(500);
            await sleep(2000);

            const playAgainButton = findButton('Play Again');
            if (playAgainButton) {
                while (!clickElement(playAgainButton)) await sleep(500);
                await sleep(3000);
                await waitForInputFocusAndNewWord();
                triggerSingleTab();
                continue;
            }
        }

        const wordElems = document.querySelectorAll('div[class*="text-"]');
        const activeWord = Array.from(wordElems).find(el =>
            el.innerText.trim().length > 0 &&
            window.getComputedStyle(el).color === 'rgb(255, 255, 255)'
        );

        if (!activeWord) {
            await sleep(1000);
            continue;
        }

        const word = activeWord.innerText.trim();
        console.log(`📝 正在输入: ${word}`);
        let current = '';
        for (const char of word) {
            current += char;
            triggerInput(input, current);
            await sleep(80 + Math.random() * 20);
        }

        triggerInput(input, current + ' ');
        await sleep(200);

        if (wordElems.length === 1) {
            await triggerDoubleTab(); // 优化：直接调用双 Tab 模拟
            await sleep(1000);

            // 备用机制：如果双 Tab 无效，尝试点击 Play Again 按钮
            const playAgainButton = findButton('Play Again');
            if (playAgainButton) {
                console.log("🔄 双 Tab 可能失败，尝试点击 Play Again 按钮");
                while (!clickElement(playAgainButton)) await sleep(500);
                await sleep(3000);
                await waitForInputFocusAndNewWord();
                triggerSingleTab();
            }
        }

        await sleep(500);
    }
})();
