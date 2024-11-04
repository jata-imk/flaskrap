import React from 'react';
import { Card, CardBody } from "@nextui-org/card";
import { IoSparklesSharp } from "react-icons/io5";

const AIPrompt = ({ prompt }) => {
  return (
    <Card className="bg-gradient-to-r from-purple-400 to-pink-500">
      <CardBody className="flex flex-col p-4">
        <div className="flex items-center mb-2">
          <IoSparklesSharp className="text-white text-xl mr-2" />
          <p className="text-white text-sm font-semibold">Suggestion made by AI</p>
        </div>
        <p className="text-white text-lg italic">{prompt}</p>
      </CardBody>
    </Card>
  );
};

export default AIPrompt;