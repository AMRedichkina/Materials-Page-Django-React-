import styles from './style.module.css';
import React, { useEffect, useRef, useState } from 'react';
import GLOBE from 'vanta/dist/vanta.globe.min';
import * as THREE from 'three';

const Background = ({ children }) => {
    const [vantaEffect, setVantaEffect] = useState(0);
    const ref = useRef(null);

    useEffect(() => {
        if (!vantaEffect) {
            setVantaEffect(GLOBE({
                el: ref.current,
                mouseControls: true,
                touchControls: true,
                gyroControls: false,
                minHeight: 200.00,
                minWidth: 200.00,
                scale: 1.00,
                scaleMobile: 1.00,
                color: 0xceceff,
                color2: 0xcbd9ff,
                size: 2.00,
                backgroundColor: 0xffffff,
                THREE
            }));
        }
        return () => {
            if (vantaEffect) vantaEffect.destroy();
        };
    }, [vantaEffect]);

    return <div ref={ref} className={styles.vantaBg}>{children}</div>;
};

export default Background;
