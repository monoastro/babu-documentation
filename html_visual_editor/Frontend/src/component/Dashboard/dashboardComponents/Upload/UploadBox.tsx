import type React from "react";
import UploadArea from "./UploadArea";

type UploadBoxProps = {
  uploadImg: boolean;
  setUploadImg: React.Dispatch<React.SetStateAction<boolean>>;
  image: File | null;
  setImage: React.Dispatch<React.SetStateAction<File | null>>;
};

const UploadBox: React.FC<UploadBoxProps> = ({
  uploadImg,
  setUploadImg,
  image,
  setImage,
}) => {
  return (
    <>
      {" "}
      <div
        className={`fixed top-0 left-0 min-w-screen  bg-transparent z-40 flex flex-col items-center justify-center transition-all duration-300 ease-in-out ${
          uploadImg
            ? "h-screen opacity-100 pointer-events-auto "
            : "h-0 opacity-0 pointer-events-none scale-0"
        }`}
      >
        <div
          className={`relative w-[300px]  xl:w-[350px] h-[200px] flex justify-center items-baseline-last text-center bg-[#1C1B18] rounded-2xl py-3 px-2 ${
            uploadImg ? "animate-popup" : ""
          }`}
        >
          <button
            onClick={() => {
              setUploadImg(false);
              setImage(null);
            }}
            className="absolute top-0 right-2 text-2xl lg:text-3xl  focus:outline-none cursor-pointer text-white"
            aria-label="Close button"
          >
            &times;
          </button>
          <UploadArea image={image} setImage={setImage} />
        </div>
      </div>
    </>
  );
};

export default UploadBox;
