// Chakra imports
import { Avatar, Box, Flex, Text, useColorModeValue } from "@chakra-ui/react";
import Card from "components/card/Card.js";
import React from "react";
import { formatBytes, formatNumbers } from "assets/utils";

export default function Banner(props) {
    const { banner, avatar, name, photos, videos, usedSpace } = props;
    // Chakra Color Mode
    const textColorPrimary = useColorModeValue("secondaryGray.900", "white");
    const textColorSecondary = "gray.400";
    const borderColor = useColorModeValue(
        "white !important",
        "#111C44 !important"
    );
    return (
        <Card mb={{ base: "0px", lg: "20px" }} align='center'>
            <Box
                bg={`url(${banner})`}
                bgSize='cover'
                borderRadius='16px'
                h='131px'
                w='100%'
            />
            <Avatar
                mx='auto'
                src={avatar}
                h='87px'
                w='87px'
                mt='-43px'
                border='4px solid'
                borderColor={borderColor}
            />
            <Text color={textColorPrimary} fontWeight='bold' fontSize='xl' mt='10px'>
                {name}
            </Text>
            <Flex w='max-content' mx='auto' mt='26px'>
                <Flex mx='auto' me='60px' align='center' direction='column'>
                    <Text color={textColorPrimary} fontSize='2xl' fontWeight='700'>
                        {formatNumbers(photos)}
                    </Text>
                    <Text color={textColorSecondary} fontSize='sm' fontWeight='400'>
                        Fotos
                    </Text>
                </Flex>
                <Flex mx='auto' me='60px' align='center' direction='column'>
                    <Text color={textColorPrimary} fontSize='2xl' fontWeight='700'>
                        {formatNumbers(videos)}
                    </Text>
                    <Text color={textColorSecondary} fontSize='sm' fontWeight='400'>
                        Videos
                    </Text>
                </Flex>
                <Flex mx='auto' align='center' direction='column'>
                    <Text color={textColorPrimary} fontSize='2xl' fontWeight='700'>
                        {formatBytes(usedSpace)}
                    </Text>
                    <Text color={textColorSecondary} fontSize='sm' fontWeight='400'>
                        Espaço Utilizado
                    </Text>
                </Flex>
            </Flex>
        </Card>
    );
}
