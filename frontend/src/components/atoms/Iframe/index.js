// frontend/src/components/atoms/Iframe/index.js

function Iframe({ src, title, ...props }) {
    return <iframe src={src} title={title} {...props} />;
}

export default Iframe;
