import {
    SimpleGrid,
  } from "@chakra-ui/react";
  // Custom components
import React from "react";
import BatchProcessingTime from "views/admin/default/components/BatchProcessingTime";
import BatchProcessingVolume from "views/admin/default/components/BatchProcessingVolume";

export default function ClassifiedMediaVolume(props) {
    const {brandColor, boxBg} = props;
    return (
        <>
            <SimpleGrid columns={{ base: 1, md: 1, xl: 1 }} gap='20px' mb='20px'>
                <BatchProcessingTime />
            </SimpleGrid>
        </>
    )
}