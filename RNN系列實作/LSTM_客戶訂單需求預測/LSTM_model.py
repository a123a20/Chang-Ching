import torch
import torch.nn as nn

class LSTM(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, dropout, seq_length, use_GPU):  # 這裡加入要傳入的參數，使用時記得要加self.X = X
        super(LSTM, self).__init__()
        
        # 導入參數
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.dropout = dropout
        self.seq_length = seq_length
        self.use_GPU = use_GPU
        
        # model設計
        self.rnn = nn.LSTM(
            input_size = input_size,  # input shape
            hidden_size = hidden_size,  # output shape
            num_layers = num_layers,
            dropout = dropout
            #batch_first = True  # 只是做 原(459,7,1) -> (7,459,1)，這次沒有設batch_size，固batch_size=459 (全部data)
                                 # (batch_size, time_step, input_size) batch已經在最前面，不需再batch_first
        )
        self.out = nn.Linear(hidden_size, 1)  # (in_features, out_features)->(512, 1)
        
    def reset_hidden_state(self):  # 清空inputs的 h_0, c_0 (state)->讓每個epoch開始訓練 都是空的state
        self.h_0 = torch.zeros(self.num_layers, self.seq_length, self.hidden_size)  # 透過self，抓取外界傳入的參數(初始化需先導入)
        self.c_0 = torch.zeros(self.num_layers, self.seq_length, self.hidden_size)
        
    def forward(self, x):
        """
        x: (batch_size, time_step(seq_length), input_size)
        h_n = 最後一個time_step的 "hidden state" (輸出)   h_n = lstm_out[:,-1,:]
        c_n = 最後一個time_step的 "cell state" (cell當前狀態)
        """
        
        # 若有使用gpu，hidden tensor也需移到gpu
        if self.use_GPU == True and torch.cuda.is_available() == True:
            self.h_0, self.c_0 = self.h_0.cuda(), self.c_0.cuda()
            
        #---x: (459, 7, 1)    
        lstm_out, (self.h_n, self.c_n) = self.rnn(x, (self.h_0, self.c_0))  # 1 -> 512 
        #---lstm_out: (459, 7, 512)
        
        # 查看hidden_state (tuple → tensor)
        #hidden_state = torch.stack(list((self.h_0,self.c_0)), dim=0)  # h_n, c_n = hidden_state = (2, num_layers, 7, 512)
        #print(hidden_state.shape)  # hidden_state: ( (h,c), num_layers, time_step(seq_length), hidden_size)
        
        #---lstm_out: (459, 7, 512)
        last_time_step = lstm_out.view(self.seq_length, len(x), self.hidden_size)  # 改變數據shape (取出 7的最後一個 時間步(time_step) 的輸出)
        #---last_time_step: (7, 459, 512)
        last_time_step = last_time_step[-1]  # 取0~6的最後一列
        #---last_time_step: (459, 512)
        output = self.out(last_time_step)  # (459, 512) -> (459, 1)
        #---output: (459, 1)  # 459列 預測的結果
        return output  # y_predict

