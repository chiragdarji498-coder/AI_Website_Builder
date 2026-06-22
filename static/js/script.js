document.addEventListener('DOMContentLoaded', () => {
    // 1. Navbar Scroll Effect
    const navbar = document.getElementById('navbar');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // 2. Intersection Observer for Fade-In Elements
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    document.querySelectorAll('.fade-in').forEach(element => {
        observer.observe(element);
    });

    // 3. Dynamic Typewriter Effect for Hero Section
    const words = ["Artificial Intelligence.", "Absolute Precision.", "Unmatched Speed.", "Zero Limits."];
    let wordIndex = 0;
    let charIndex = 0;
    let isDeleting = false;
    const typewriterElement = document.getElementById('typewriter');

    function typeEffect() {
        const currentWord = words[wordIndex];
        
        if (isDeleting) {
            typewriterElement.textContent = currentWord.substring(0, charIndex - 1);
            charIndex--;
        } else {
            typewriterElement.textContent = currentWord.substring(0, charIndex + 1);
            charIndex++;
        }

        let typingSpeed = isDeleting ? 50 : 100;

        if (!isDeleting && charIndex === currentWord.length) {
            typingSpeed = 2000; // Pause at end of word
            isDeleting = true;
        } else if (isDeleting && charIndex === 0) {
            isDeleting = false;
            wordIndex = (wordIndex + 1) % words.length;
            typingSpeed = 500; // Pause before new word
        }

        setTimeout(typeEffect, typingSpeed);
    }

    // Start typewriter effect
    setTimeout(typeEffect, 1000);

    // 4. Generate Button Interaction & Workspace Logic
    const generateBtn = document.querySelector('.generate-btn');
    const promptInput = document.querySelector('.prompt-input');
    const heroSection = document.querySelector('.hero');
    const featuresSection = document.querySelector('.features-section');
    const workspace = document.getElementById('workspace');
    const codeViewer = document.getElementById('code-viewer');
    const previewFrame = document.getElementById('preview-frame');

    generateBtn.addEventListener('click', async () => {
        const prompt = promptInput.value.trim();
        if (prompt === "") {
            promptInput.style.border = "1px solid #ff5f56";
            setTimeout(() => {
                promptInput.style.border = "none";
            }, 1000);
            return;
        }
        
        // UI Loading State
        const originalText = generateBtn.textContent;
        generateBtn.innerHTML = 'Generating... (This may take a minute)';
        generateBtn.style.opacity = '0.8';
        generateBtn.disabled = true;

        try {
            // Send request to your Flask backend
            const response = await fetch('/api/generate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ prompt: prompt })
            });

            const data = await response.json();

            if (data.success) {
                // Hide Landing Page, Show Workspace
                heroSection.style.display = 'none';
                featuresSection.style.display = 'none';
                workspace.classList.remove('hidden');

                // Force iframe to reload the newly generated file
                // Using a timestamp to bypass browser caching
                const cacheBuster = new Date().getTime();
                previewFrame.src = '/static/generated/latest/index.html?t=' + cacheBuster;
                
                // Fetch the raw HTML to display in the left panel code viewer
                const codeResponse = await fetch('/static/generated/latest/index.html?t=' + cacheBuster);
                const rawCode = await codeResponse.text();
                codeViewer.textContent = rawCode;

                // Reset the generate button for next time
                generateBtn.innerHTML = originalText;
                generateBtn.style.opacity = '1';
                generateBtn.disabled = false;
                promptInput.value = '';

            } else {
                alert("Error generating website: " + data.error);
                generateBtn.innerHTML = originalText;
                generateBtn.style.opacity = '1';
                generateBtn.disabled = false;
            }
        } catch (error) {
            console.error("Fetch error:", error);
            alert("Could not connect to the server.");
            generateBtn.innerHTML = originalText;
            generateBtn.style.opacity = '1';
            generateBtn.disabled = false;
        }
    });

    // 5. Device Preview Resizing Logic
    const btns = document.querySelectorAll('.device-toggles button:not(#view-fullscreen)');
    
    document.getElementById('view-desktop').addEventListener('click', (e) => {
        previewFrame.style.width = '100%';
        setActiveBtn(e.target);
    });
    
    document.getElementById('view-tablet').addEventListener('click', (e) => {
        previewFrame.style.width = '768px';
        setActiveBtn(e.target);
    });
    
    document.getElementById('view-mobile').addEventListener('click', (e) => {
        previewFrame.style.width = '375px';
        setActiveBtn(e.target);
    });

    function setActiveBtn(clickedBtn) {
        btns.forEach(btn => btn.classList.remove('active'));
        clickedBtn.classList.add('active');
    }

    // 6. Copy Code Button Logic
    const copyBtn = document.querySelector('.copy-btn');
    if (copyBtn) {
        copyBtn.addEventListener('click', () => {
            navigator.clipboard.writeText(codeViewer.textContent).then(() => {
                const originalBtnText = copyBtn.textContent;
                copyBtn.textContent = 'Copied!';
                copyBtn.style.background = 'rgba(39, 201, 63, 0.2)';
                copyBtn.style.borderColor = '#27c93f';
                
                setTimeout(() => {
                    copyBtn.textContent = originalBtnText;
                    copyBtn.style.background = '';
                    copyBtn.style.borderColor = '';
                }, 2000);
            });
        });
    }

    // 7. Back Button Logic
    const backBtn = document.getElementById('back-btn');
    if (backBtn) {
        backBtn.addEventListener('click', () => {
            // Hide workspace
            workspace.classList.add('hidden');
            
            // Show landing page sections
            heroSection.style.display = 'flex';
            featuresSection.style.display = 'block';
            
            // Smoothly scroll back to the top
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    // 8. Full Screen Logic for Iframe
    const fullscreenBtn = document.getElementById('view-fullscreen');
    if (fullscreenBtn) {
        fullscreenBtn.addEventListener('click', () => {
            // Check browser compatibility for Fullscreen API
            if (previewFrame.requestFullscreen) {
                previewFrame.requestFullscreen();
            } else if (previewFrame.webkitRequestFullscreen) { /* Safari */
                previewFrame.webkitRequestFullscreen();
            } else if (previewFrame.msRequestFullscreen) { /* IE11 */
                previewFrame.msRequestFullscreen();
            } else if (previewFrame.mozRequestFullScreen) { /* Firefox */
                previewFrame.mozRequestFullScreen();
            }
        });
    }
});