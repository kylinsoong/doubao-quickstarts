package com.bytedance.demo;

import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import com.volcengine.ark.runtime.model.completion.chat.ChatCompletionContentPart;
import com.volcengine.ark.runtime.model.completion.chat.ChatCompletionRequest;
import com.volcengine.ark.runtime.model.completion.chat.ChatMessage;
import com.volcengine.ark.runtime.model.completion.chat.ChatMessageRole;
import com.volcengine.ark.runtime.service.ArkService;
import okhttp3.ConnectionPool;
import okhttp3.Dispatcher;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.TimeUnit;


@SpringBootApplication
public class Main implements CommandLineRunner {

	

	public static void main(String[] args) {
		SpringApplication.run(Main.class, args);
	}
	
	 static String apiKey = System.getenv("ARK_API_KEY");
    // 此为默认路径，您可根据业务所在地域进行配置
    static String baseUrl = "https://ark.cn-beijing.volces.com/api/v3";
    static ConnectionPool connectionPool = new ConnectionPool(5, 1, TimeUnit.SECONDS);
    static Dispatcher dispatcher = new Dispatcher();
    static ArkService service = ArkService.builder().dispatcher(dispatcher).connectionPool(connectionPool).baseUrl(baseUrl).apiKey(apiKey).build();
	
    static String videoPath = "/Users/bytedance/Downloads/001.mp4";

    static String encodeVideo(String videoPath) throws IOException {
        byte[] videoBytes = Files.readAllBytes(Paths.get(videoPath));
        return java.util.Base64.getEncoder().encodeToString(videoBytes);
    }
  
	@Override
	public void run(String... args) throws Exception {

        System.out.println("----- vedio input(vedio from local path) -----");

        final List<ChatMessage> messages = new ArrayList<>();
        final List<ChatCompletionContentPart> multiParts = new ArrayList<>();
        multiParts.add(ChatCompletionContentPart.builder().type("video_url").videoUrl(
                new ChatCompletionContentPart.ChatCompletionContentPartVideoURL(
                        "data:video/mp4;base64," + encodeVideo(videoPath),
                        1 
                )
        ).build());

        
        multiParts.add(ChatCompletionContentPart.builder().type("text").text(
                "视频中有什么？"
        ).build());

        final ChatMessage userMessage = ChatMessage.builder().role(ChatMessageRole.USER)
                .multiContent(multiParts).build();
        messages.add(userMessage);

        ChatCompletionRequest chatCompletionRequest = ChatCompletionRequest.builder()
                .model("ep-20251127204045-sbczk")
                .messages(messages)
                .build();

        service.createChatCompletion(chatCompletionRequest).getChoices().forEach(choice -> System.out.println(choice.getMessage().getContent()));

        service.shutdownExecutor();
		
	}

}
