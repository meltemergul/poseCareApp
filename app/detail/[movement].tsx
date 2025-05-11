import { useLocalSearchParams, useRouter } from "expo-router";
import { Image, Pressable, Text, View } from "react-native";

export default function MovementDetail() {
    const { movement } = useLocalSearchParams();
    const router = useRouter();
    const getImage = () => {
        if (movement === "Squat") {
            return require("../../assets/images/squat.jpg");
        } else if (movement === "Bridge") {
            return require("../../assets/images/bridge.jpg");
        } else {
            return require("../../assets/images/icon.png"); // yedek resim
        }
    };
    return (
        <View style={{ flex: 1, backgroundColor: "#000", padding: 24 }}>
            <Text style={{ color: "#fff", fontSize: 22, marginBottom: 16 }}>{movement}</Text>

            <Image
                source={getImage()}
                style={{ width: "100%", height: 200, borderRadius: 12, marginBottom: 16 }}
            />


            <Text style={{ color: "#ccc", marginBottom: 24 }}>
                Bu egzersiz karın, kalça ve sırt kaslarını çalıştırır. Yere uzanıp ayaklarınızı kaldırarak yapın.
            </Text>

            <Pressable
                onPress={() => router.push("/exercise")}
                style={{ backgroundColor: "#B0FF35", padding: 16, borderRadius: 10 }}
            >
                <Text style={{ textAlign: "center", fontWeight: "bold" }}>Başla</Text>
            </Pressable>
        </View>
    );
}
