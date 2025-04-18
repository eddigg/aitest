import React from 'react';
import Lottie from 'react-lottie';

export const LottieLoader = ({ animationData, width = 100, height = 100, loop = true, autoplay = true }) => {
  const defaultOptions = {
    loop,
    autoplay,
    animationData,
    rendererSettings: {
      preserveAspectRatio: 'xMidYMid slice'
    }
  };

  return (
    <div style={{ width, height }}>
      <Lottie
        options={defaultOptions}
        height={height}
        width={width}
        isStopped={false}
        isPaused={false}
      />
    </div>
  );
};

// Usage example:
// import loadingAnimation from '../assets/loading.json';
// <LottieLoader animationData={loadingAnimation} width={200} height={200} />