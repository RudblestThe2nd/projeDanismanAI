import pusulaImg from "../assets/pusula.png";

export default function CompassSVG({ size = "small" }) {
  const dim = size === "large" ? 98 : 70;
  return (
    <img
      src={pusulaImg}
      width={dim}
      height={dim}
      alt="Pusula"
      style={{ display: "block", objectFit: "contain" }}
    />
  );
}
