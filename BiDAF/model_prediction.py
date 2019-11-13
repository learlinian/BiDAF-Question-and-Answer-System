from torch import nn, optim
from model.model import BiDAF
from model.data import SQuAD
from time import gmtime, strftime
import argparse
import torch
import json
import time
import os


def predict():
    parser = argparse.ArgumentParser()
    parser.add_argument('--char-dim', default=8, type=int)
    parser.add_argument('--char-channel-width', default=5, type=int)
    parser.add_argument('--char-channel-size', default=100, type=int)
    parser.add_argument('--context-threshold', default=400, type=int)
    parser.add_argument('--dev-batch-size', default=100, type=int)
    parser.add_argument('--test-batch-size', default=100, type=int)
    parser.add_argument('--dev-file', default='dev-v1.1.json')
    parser.add_argument('--test-file', default='test1.json')
    parser.add_argument('--dropout', default=0.2, type=float)
    parser.add_argument('--epoch', default=12, type=int)
    parser.add_argument('--exp-decay-rate', default=0.999, type=float)
    parser.add_argument('--gpu', default=0, type=int)
    parser.add_argument('--hidden-size', default=200, type=int)
    parser.add_argument('--learning-rate', default=0.5, type=float)
    parser.add_argument('--print-freq', default=250, type=int)
    parser.add_argument('--train-batch-size', default=60, type=int)
    parser.add_argument('--train-file', default='train-v1.1.json')
    parser.add_argument('--word-dim', default=300, type=int)
    args = parser.parse_args()


    print('loading SQuAD data...')
    current_dir = os.getcwd()
    current_dir = os.path.join(current_dir, 'BiDAF')
    path = os.path.join(current_dir, 'testing_files')
    data = SQuAD(args, path)
    setattr(args, 'char_vocab_size', len(data.CHAR.vocab))
    setattr(args, 'word_vocab_size', len(data.WORD.vocab))
    setattr(args, 'dataset_file', f'testing_files/{args.dev_file}')
    setattr(args, 'prediction_file', f'output/prediction{time.time()}.out')
    setattr(args, 'model_time', strftime('%H:%M:%S', gmtime()))
    print('data loading complete!')

    device = torch.device(f"cuda:{args.gpu}" if torch.cuda.is_available() else "cpu")
    model = BiDAF(args, data.WORD.vocab.vectors).to(device)

    # load trained the parameters to the model
    model_path = os.path.join(current_dir, 'saved_models')
    model.load_state_dict(torch.load(os.path.join(model_path, 'BiDAF_tl_new.pt')))
    model.eval()    # show the model result

    answers = dict()    # answers to be saved in dictionary format
    with torch.set_grad_enabled(False):
        for batch in iter(data.test_iter):
            # print(batch)
            p1, p2 = model(batch)
            # batch_loss = criterion(p1, batch.s_idx) + criterion(p2, batch.e_idx)
            # loss += batch_loss.item()

            batch_size, c_len = p1.size()
            ls = nn.LogSoftmax(dim=1)
            mask = (torch.ones(c_len, c_len) * float('-inf')).to(device).tril(-1).unsqueeze(0).expand(batch_size, -1, -1)
            score = (ls(p1).unsqueeze(2) + ls(p2).unsqueeze(1)) + mask
            score, s_idx = score.max(dim=1)
            score, e_idx = score.max(dim=1)
            s_idx = torch.gather(s_idx, 1, e_idx.view(-1, 1)).squeeze()
            for i in range(batch_size):
                id = batch.id[i]
                answer = batch.c_word[0][i][s_idx[i]:e_idx[i] + 1]
                answer = ' '.join([data.WORD.vocab.itos[idx] for idx in answer])
                answers[id] = answer

    print(answers)
    return answers
