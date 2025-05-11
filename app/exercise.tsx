import { Image, Text, View } from "react-native";

export default function ExerciseScreen() {
    return (
        <View style={{ flex: 1, backgroundColor: "#000", padding: 24 }}>
            <Image
                source={{ uri: "https://via.placeholder.com/squat" }}
                style={{ width: "100%", height: 300, borderRadius: 12, borderWidth: 3, borderColor: "#B0FF35" }}
            />

            <Text style={{ color: "#fff", fontSize: 18, marginTop: 24 }}>Doğru: 5</Text>
            <Text style={{ color: "#fff", fontSize: 18 }}>Yanlış: 2</Text>
            <Text style={{ color: "#fff", fontSize: 18, marginTop: 12 }}>Durum: Squat</Text>
        </View>
    );
}
