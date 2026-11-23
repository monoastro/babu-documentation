type UploadAreaProps = {
  image: File | null;
  setImage: React.Dispatch<React.SetStateAction<File | null>>;
};

const UploadArea: React.FC<UploadAreaProps> = ({ image, setImage }) => {
  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0]; // only first file
    if (file && file.type.startsWith("image/")) {
      setImage(file);
    } else {
      alert("Please drop an image file only.");
    }
  };

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
  };
  return (
    <>
      <div
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        className="w-full h-40 border-2 border-dashed border-[#00FFBB] 
                 flex items-center justify-center 
                 text-[#00FFBB] bg-[#1C1B18] rounded-md cursor-pointer"
      >
        {image ? (
          <div className="text-center">
            <p className="font-medium">{image.name}</p>
            <img
              src={URL.createObjectURL(image)}
              alt="preview"
              className="mt-2 max-h-24 mx-auto rounded"
            />
          </div>
        ) : (
          <p>Drag & drop an image here</p>
        )}
      </div>
    </>
  );
};

export default UploadArea;
